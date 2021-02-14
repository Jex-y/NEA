using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using System.Diagnostics;
using Xamarin.Forms;
using hollywood.Services;
using hollywood.Models;
using hollywood.Views;
using System.Collections.ObjectModel;

namespace hollywood.ViewModels
{
    class BasketPageViewModel : BaseViewModel
    {
        readonly IContextService contextService;
        readonly IRestService restService;

        readonly ICommand _getSessIdCommand;
        readonly ICommand _submitOrderCommand;
        readonly string _submitOrderText = "Order";
        readonly string _getSessIdText = "Scan code";
        ObservableCollection<Item> _items;
        bool _canOrder;
        bool _hasItems;

        public BasketPageViewModel() 
        {
            contextService = DependencyService.Get<IContextService>();
            restService = DependencyService.Get<IRestService>();
            Items = new ObservableCollection<Item>();
               
            Debug.WriteLine("Got here");

            UpdateItems();

            _getSessIdCommand = new Command(async () => await GetSessId());
            _submitOrderCommand = new Command(async () => await SubmitOrder());
        }

        public ICommand ButtonCommand 
        {
            get { return CanOrder ? _submitOrderCommand : _getSessIdCommand; }
        }

        public string ButtonText 
        {
            get { return CanOrder ? _submitOrderText : _getSessIdText; }
        }

        public ObservableCollection<Item> Items 
        {
            get { return _items; }
            set { SetProperty(ref _items, value); }
        }

        public bool CanOrder 
        {
            get { return !(contextService.Context.CurrentSession is null) && HasItems; }
        }

        public bool HasItems 
        {
            get { return !(contextService.Context.Basket.Items.Count == 0); }
        }

        async Task GetSessId() 
        {
            IQrScannerService qrScanner = DependencyService.Get<IQrScannerService>();
            string sessId = await qrScanner.readCode();
            if (await ValidateSessId(sessId))
            {
                IContextService contextService = DependencyService.Get<IContextService>();
                contextService.Context.CurrentSession = new Session { SessId = new Guid(sessId) };
            }
            else
            {
                Debug.WriteLine("Could not scan qr code");
            }
        }

        async Task SubmitOrder() 
        {
            if (await restService.SubmitOrder(contextService.Context.Basket, contextService.Context.CurrentSession))
            {
                contextService.Context.Basket = new Order();
                UpdateItems();
            }
            else
            {
                Debug.WriteLine("Could not submit order");
            }
        }

        async Task<bool> ValidateSessId(string sessId)
        {
            return await restService.ValidateSessId(sessId);
        }

        async Task UpdateItems() 
        {
            bool startEmpty = Items.Count == 0;
            int i = 0;
            if (contextService.Context.Basket.Items.Count == 0)
            {
                Items = new ObservableCollection<Item>();
            }
            else 
            {
                foreach (Guid itemId in contextService.Context.Basket.Items.Keys)
                {
                    if (startEmpty)
                    {
                        _items.Add(null);
                    }
                    GetItem(itemId, i);
                    i++;
                }
            }
            
        }

        async Task GetItem(Guid itemId, int index) 
        {
            Items.Insert(index, restService.GetItemDetail(itemId).Result);
        }

    }
}
