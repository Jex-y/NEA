import datetime
import uuid
from django.http import Http404
from django.db.models import Q
from django.utils import timezone
from django.core import exceptions
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models
from . import serializers

class ItemSearchView(APIView):
    """
    API method to search item menus and descriptions

    Meets requirements: 2.10
    '''

    Attributes
    --------
    None

    Methods
    --------
    get_objects(self, query):
        Queries the database and returns revelant items

    get(self, request, query):
        Serves the API method

    """

    def get_objects(self, query):
        """
        Queries the database and returns revelant items

        Parameters:
            query (str): the search query

        Returns:
            (QuerySet): Items where either the name or description match the search query.
                        May return empty if query does not match any.

        Raises:
            Http404: Database query failed

        """
        try:
            return models.Item.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        except:
            raise Http404

    def get(self, request, query):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method
            query (str): the search query URL parameter

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        items = self.get_objects(query)
        serializer = serializers.ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

class ItemFilterView(APIView):
    """
    API method to return all the items matched by a set of tags
    Meets requirements: Needed for 1.09
    '''

    Attributes
    --------

    Methods
    --------
    get_objects(self, tags):
        Queries the database and returns item where they contain at least one of many given tags

    get(self, request, tags=None):
        Serves the API method

    """

    def get_objects(self, tags):
        """
        Queries the database and returns revelant items

        Parameters:
            tags ([str]): list of the tags to filter by

        Returns:
            (QuerySet): all items that have any of the tags passed

        Raises:
            Http404: Database query failed or tags were invalid

        """
        try:
            query = Q()
            # Returns matches for any of the tags
            for tag in tags:
                query = query | Q(tags__id=tag)

            itemSet = set(models.Item.objects.filter(query))
            # Set removes duplicates
            return itemSet
        except:
            raise Http404 # Something was wrong with the query

    def get(self, request, tags=None):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method
            tags (str): the tags to filter by, seperated by '&'

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        items = self.get_objects(tags.split('&'))
        serializer = serializers.ItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)

class ItemMenuListView(APIView):
    """
    API method that returns a list of items and menus in a menu
    Meets requirements: 2.08, 2.09
    '''

    Attributes
    --------

    Methods
    --------
    get_objects(self, query):
        Queries the database and returns all items and submenus in a given menu where they are available

    get(self, request, url_name):
        Serves the API method

    """

    # This is a static variable used to test the view at different times
    test_time = None

    def get_objects(self, url_name):
        """
        Queries the database and returns items and menus that are contained by the given menu. 
        Note that the url_nane does not have to be unique. 
        There could be two menus of same name and the results would be merged. 
        The use case for this would be if there are certain items in a menu that needed to be scheduled or removed together.

        Parameters:
            url_name (str): The URL name of the menu to get the items of.

        Returns:
            (QuerySet): items in the given menu
            (QuerySet): menus in the given menu
        Raises:
            Http404: Database query failed

        """
        try:
            # Could be vulnerable to SQL injection from url_name
            if isinstance(ItemMenuListView.test_time, datetime.datetime):
                now = ItemMenuListView.test_time
            else:
                now = timezone.now()
            
            time = str(now.time())
            dayofweek = str(now.weekday())
            if url_name:
                menus = models.Menu.objects.raw(f"""
                    SELECT child.* FROM backend_menu child, backend_menu parent WHERE
                        parent.url_name = '{url_name}' AND
                        child.super_menu_id = parent.id AND
                        child.available = 1 AND
	                    (	
		                    ( child.start_time IS NULL OR child.start_time <= '{time}' ) AND 
		                    ( child.end_time IS NULL OR child.end_time >= '{time}' )
	                    ) AND
	                    (	
		                    ( child.start_day IS NULL OR child.start_day <= {dayofweek} ) AND 
		                    ( child.end_day IS NULL OR child.end_day >= {dayofweek} )
	                    )
                """)
                items = models.Item.objects.raw(f"""
                    SELECT item.* FROM backend_item item, backend_menu menu, backend_menu_items WHERE
	                    url_name = '{url_name}' AND 
	                    menu_id = menu.id AND 
	                    item.id = item_id AND
                        item.available = 1
                """)
            else:
                menus = models.Menu.objects.raw(f"""
                    SELECT * FROM backend_menu WHERE
                        super_menu_id IS NULL AND
                        available = 1 AND
	                    (	
		                    ( start_time IS NULL OR start_time <= '{time}' ) AND 
		                    ( end_time IS NULL OR end_time >= '{time}' )
	                    ) AND
	                    (	
		                    ( start_day IS NULL OR start_day <= {dayofweek} ) AND 
		                    ( end_day IS NULL OR end_day >= {dayofweek} )
	                    )
                """)

                items = models.Item.objects.none()
                
            return menus, items

        except Exception as e:
            print(e)
            raise Http404
        
    def get(self, request, url_name=None):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method
            query: (url_name): the url_name for the menu. If not given defualts to top level

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        menus, items = self.get_objects(url_name)
        menu_serializer = serializers.MenuSerializer(menus, many=True, context={"request": request})
        item_serializer = serializers.ItemSerializer(items, many=True, context={"request": request})
        data = {
            'menus': menu_serializer.data,
            'items': item_serializer.data,
            }
           
        return Response(data)

class ItemDetailView(APIView):
    """
    API method to return the details of an item given its item id
    Meets requirements: 
    '''

    Attributes
    --------

    Methods
    --------
    get_objects(self, query):
        Queries the database and returns an item with matching item id

    get(self, request, item_id):
        Serves the API method

    """
    def get_objects(self, item_id):
        """
        Queries the database and returns the item given the item id

        Parameters:
            item_id (str): uuid4 item id

        Returns:
            (Item): item with correct item id

        Raises:
            Http404: Database query failed

        """
        try:
            item = models.Item.objects.get(id=item_id)
            return item
        except Exception as e:
            raise Http404

    def get(self, request, item_id):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method
            item_id (str): the item id of the item

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        item = self.get_objects(item_id)
        serializer = serializers.ItemSerializer(item, context={'request': request})
        return Response(serializer.data)

class SessionCreateView(APIView):
    """
    API method to start a session for a given table and return its session id
    Meets requirements:
    '''

    Attributes
    --------
    None

    Methods
    --------
    post(self, request):
        Serves the API method

    """
    def post(self, request):
        """
        Serves the API method. Created the session in the database and returns it's session id.

        Parameters:
            request (HttpRequest): the request that called the API method

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        table_num = request.POST.get('table_num')

        try:
            table_num = int(table_num)
        except:
            table_num = None

        if not table_num:
            data = {
                'result':'Error: Parametrs not understood',
                'sessid':None,
                }

            requestStatus = status.HTTP_400_BAD_REQUEST

        elif models.Session.objects.filter(table=table_num, end_time=None).count() > 0:
            data = {
                'info':'Error: Open session already exsists for that table',
                'sessid':None,
                }

            requestStatus = status.HTTP_409_CONFLICT

        else:
            try:
                table = models.Table.objects.get(table_number = table_num)

                sess = models.Session.objects.create(table=table)

                data = {
                    'info':'Session created',
                    'sessid':sess.sessId,
                    }

                requestStatus = status.HTTP_201_CREATED
            except:
                data = {
                    'info':f'Error: table with number {table_num} does not exist',
                    'sessid':None
                    }

                requestStatus = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data, requestStatus)

class SessionValidateView(APIView):
    """
    API Method to validate that a session id is valid
    Meets requirements:
    '''

    Attributes
    --------
    None

    Methods
    --------
    valid_uuid4(self, value):
        Validates if a string is a uuid4

    post(self, request):
        Serves the API method

    """
    def valid_uuidV4(self, value):
        """
        Validates if a string is a uuid4

        Parameters:
            value (str): string to be checked

        Returns:
            (bool): if the string is a valid uuid4
        """
        value = str(value)
        try:
            test_uuid = uuid.UUID(value, version=4)
            assert(str(test_uuid) == value)
            result = True
        except (ValueError, AssertionError):
            result = False
        return result
    
    def post(self, request):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        # TODO: Check tables aswell?
        
        valid = False
        msg = 'Request format incorrect'
        requestStatus = status.HTTP_400_BAD_REQUEST
        sessId = request.POST.get('sessId')
        if self.valid_uuidV4(sessId):
            try:
                sess = models.Session.objects.get(sessId=sessId)
                if sess.start_time <= timezone.now() and sess.end_time is None and not (sess.start_time <= timezone.now() - datetime.timedelta(hours=12)):
                    # Check that start time is before now, session has not been closed and the session has not been opened more than 12 hours ago
                    msg = 'Session valid'
                    valid = True
                    requestStatus = status.HTTP_200_OK
                else:
                    msg = 'Session time invalid'
                    requestStatus = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE

            except exceptions.ObjectDoesNotExist:
                msg = f'No session with sessId={sessId} found in database'
                requestStatus = status.HTTP_404_NOT_FOUND

        data = {
            'info': msg,
            'valid':valid,
            }

        return Response(data, requestStatus)

class OrderCreateView(APIView):
    """
    API method to create an order in the database given a session id and the item orders in it
    Meets requirements: 2.11
    '''

    Attributes
    --------
    None

    Methods
    --------
    validate_json(self, json):
        Validates that the json given has the correct attributes

    post(self, request):
        Serves the API method

    """
    def validate_json(self,json):
        try:
            sessid = json['sessId']
            items = json['order']['items']
            valid = True
        except KeyError:
            valid = False
        return valid


    def post(self, request):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method
        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        json = request.data

        requestStatus = status.HTTP_400_BAD_REQUEST

        if self.validate_json(json):
            try:
                if len(json['order']['items']) == 0:
                    requestStatus = status.HTTP_406_NOT_ACCEPTABLE

                else:
                    order = models.Order.objects.create(
                        session=models.Session.objects.get(sessId=json['sessId']))

                    for item in json['order']['items']:
                        num = json['order']['items'][item]['num']
                        notes = json['order']['items'][item]['notes']
                        itemOrder = models.ItemOrder.objects.create(
                            order=order,
                            item=models.Item.objects.get(id=item),
                            quantity=num,
                            notes=notes,
                            )
                    requestStatus = status.HTTP_204_NO_CONTENT

            except (exceptions.ObjectDoesNotExist, exceptions.ValidationError):
                requestStatus = status.HTTP_400_BAD_REQUEST

        return Response(status=requestStatus)

class TagListView(APIView):
    """
    API method to return all the tags in the database.
    Meets requirements:
    '''

    Attributes
    --------
    None

    Methods
    --------
    get_objects(self, query):
        Queries the database and returns tags

    get(self, request):
        Serves the API method

    """
    def get_objects(self):
        """
        Queries the database and returns tags

        Parameters:
            None

        Returns:
            (QuerySet): All tags
        Raises:
            Http404: Database query failed

        """
        try:
            tags = models.Tag.objects.all()
            # TODO: Could fliter by if referenced by any items
            return tags
        except exception as e:
            raise Http404

    def get(self, request):
        tags = self.get_objects()
        serializer = serializers.TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

class ItemOrderListView(APIView):
    """
    API method to list items, quantities, notesn tables and itemorder ids to display to staff.
    Meets requirements:
    '''

    Attributes
    --------
    None

    Methods
    --------
    get_objects(self):
        Queries the database and returns itemorder id, name, quantity, notes and table number sorted by the oldest first.

    get(self, request, query):
        Serves the API method

    """
    def query_database(self):
        """
        Queries the database and returns itemorder id, name, quantity, notes and table number sorted by the oldest first.
        SQL query run is:
            SELECT backend_itemorder.id, name, quantity, notes, table_id FROM backend_item, backend_itemorder, backend_order, backend_session WHERE
	            completed = 0 AND
	            backend_item.id = backend_itemorder.item_id AND
	            backend_order.id = backend_itemorder.order_id AND 
	            backend_order.session_id = backend_session.sessId 
	            ORDER BY backend_order.submitted

        Parameters:
            None

        Returns:
            ([str, str, int, str, int]): item orders to be diplayed

        Raises:
            Http404: Database query failed

        """
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT backend_itemorder.id, name, quantity, notes, table_id FROM backend_item, backend_itemorder, backend_order, backend_session WHERE
	            completed = 0 AND
	            backend_item.id = backend_itemorder.item_id AND
	            backend_order.id = backend_itemorder.order_id AND 
	            backend_order.session_id = backend_session.sessId 
	            ORDER BY backend_order.submitted
            """)
            rows = cursor.fetchall()
            return rows

    def get(self, request):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        itemOrders = self.query_database()
        data = []
        for id, name, quantity, notes, table in itemOrders:
            data.append({
                        'id':str(uuid.UUID(id)),
                        'name':name,
                         'quantity':quantity,
                         'notes':notes,
                         'table':table
                         })
        return Response(data)

class ItemOrderCompleteView(APIView):
    """
    API method to mark an item order as complete in the database
    Meets requirements:
    '''

    Attributes
    --------
    None

    Methods
    --------
    get_objects(self, query):
        Queries the database and returns revelant items

    post(self, request):
        Serves the API method

    """
    def post(self, request):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method
            query: (str): the search query URL parameter

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        id = request.data['id']
        requestStatus = status.HTTP_400_BAD_REQUEST
        try:
            itemOrder = models.ItemOrder.objects.get(id=id)
            itemOrder.completed = True
            itemOrder.save()
            requestStatus = status.HTTP_202_ACCEPTED
        except (exceptions.ObjectDoesNotExist, exceptions.ValidationError):
            requestStatus = status.HTTP_400_BAD_REQUEST

        return Response(status=requestStatus)

class SessionOrderListView(APIView):
    """
    API method to list all the item orders created in a given session
    Meets requirements:
    '''

    Attributes
    --------
    None

    Methods
    --------
    query_database(self, sess_id):
        Queries the database and returns item order name, quantity, notes, completed and price

    get(self, request, sess_id):
        Serves the API method

    """
    def query_database(self, sess_id):
        """
        Queries the database and returns item order name, quantity, notes, completed and price.
        SQL query:
            SELECT name, quantity, notes, completed, price FROM backend_item, backend_itemorder, backend_order WHERE
	            backend_itemorder.item_id = backend_item.id AND 
	            backend_itemorder.order_id = backend_order.id AND 
	            backend_order.session_id = "{sess_id}"
            

        Parameters:
            sess_id (str): sess id to get item orders for

        Returns:
            ([str, int, str, bool]): item orders name, quantity, notes, completed and price 

        """
        sess_id = sess_id.replace('-','')
        with connection.cursor() as cursor:
            cursor.execute(f"""
            SELECT name, quantity, notes, completed, price FROM backend_item, backend_itemorder, backend_order WHERE
	            backend_itemorder.item_id = backend_item.id AND 
	            backend_itemorder.order_id = backend_order.id AND 
	            backend_order.session_id = "{sess_id}"
            """)
            rows = cursor.fetchall()
            return rows

    def get(self, request, sess_id):
        """
        Serves the API method

        Parameters:
            request (HttpRequest): the request that called the API method
            sess_id: (str): uuid session id to get item orders for

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        itemOrders = self.query_database(sess_id)
        data = []
        for name, quantity, notes, completed, price in itemOrders:
            data.append({
                         'name':name,
                         'quantity':quantity,
                         'notes':notes,
                         'completed':completed,
                         'total':price*quantity
                         })
        return Response(data)

class SessionCloseView(APIView):
    """
    API method to close a session. 
    Meets requirements:
    '''

    Attributes
    --------
    None

    Methods
    --------
    post(self, request):
        Serves the API method

    """
    def post(self, request):
        """
        Serves the API method. Sets the end_time of given session to current time.

        Parameters:
            request (HttpRequest): the request that called the API method

        Returns:
            (HttpResponse): API method response with JSON data
            
        """
        id = request.POST.get('sessId')
        requestStatus = status.HTTP_400_BAD_REQUEST
        try:
            sess = models.Session.objects.get(sessId=id)
            sess.end_time = timezone.now()
            sess.save()
            requestStatus = status.HTTP_202_ACCEPTED
        except (exceptions.ObjectDoesNotExist, exceptions.ValidationError):
            requestStatus = status.HTTP_400_BAD_REQUEST

        return Response(status=requestStatus)


               