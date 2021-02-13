using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using System.Net.Http;
using Newtonsoft.Json;
using Xamarin.Forms;
using Xamarin.Essentials;

using hollywood.Services;
using hollywood.Models;

using Menu = hollywood.Models.Menu;
using Debug = System.Diagnostics.Debug;
using Application = Android.App.Application;

[assembly: Dependency(typeof(hollywood.Droid.Services.RestService))]
namespace hollywood.Droid.Services
{
    class RestService : IRestService
    {
        readonly HttpClient client;
        public RestService() 
        {
            client = new HttpClient();
        }

        /// <summary>
        /// Gets menu from the server using REST API.
        /// Gets top level if handle is null otherwise gets the menu decribed by handle
        /// </summary>
        /// <param name="handle">The menu handle assosiated with the menu to get.</param>
        /// <returns>Task returning a Menu object</returns>
        public async Task<Menu> GetMenuAsync(MenuHandle handle)
        {
            Uri uri = new Uri(Constants.RestUrl + "menus/" + handle.UrlName);
            Menu menu = null;
            try
            {
                HttpResponseMessage response = await client.GetAsync(uri);
                if (response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    menu = JsonConvert.DeserializeObject<Menu>(content);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                await WarnUserCannotConnect();
            }

            return menu;
        }

        public async Task<ObservableCollection<Item>> GetSearchResults(string searchTerm)
        {
            Uri uri = new Uri(Constants.RestUrl + "items/search=" + searchTerm);
            ObservableCollection<Item> results = null;
            try
            {
                HttpResponseMessage response = await client.GetAsync(uri);
                if (response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    results = JsonConvert.DeserializeObject<ObservableCollection<Item>>(content);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex;
            }

            return results;
        }

        public async Task<ObservableCollection<Item>> GetFilterResults(ObservableCollection<Tag> tags) 
        {
            string query = tags.First().ToString();
            foreach (Tag tag in tags.Skip(1)) 
            {
                query += '&' + tag.ToString();
            }
            Uri uri = new Uri(Constants.RestUrl + "items/filter/tags=" + query);
            ObservableCollection<Item> results = null;
            try
            {
                HttpResponseMessage response = await client.GetAsync(uri);
                if (response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    results = JsonConvert.DeserializeObject<ObservableCollection<Item>>(content);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex;
            }

            return results;
        }

        public async Task<Item> GetItemDetail(Guid itemId) 
        {
            Uri uri = new Uri(Constants.RestUrl + "items/" + itemId.ToString());
            Item result = null;
            try
            {
                HttpResponseMessage response = client.GetAsync(uri).Result;
                if (response.IsSuccessStatusCode)
                {
                    string content = response.Content.ReadAsStringAsync().Result;
                    result = JsonConvert.DeserializeObject<Item>(content);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex;
            }

            return result;
        }


        /// <summary>
        /// Makes a post request to the server with a given sess id to check that:
        ///     * The sess id is a valid Guid V4
        ///     * The sess id belongs to a session that is in the database
        ///     * The session identied has not been opened in the future and has not been closed
        /// </summary>
        /// <param name="sessId">The session id to check</param>
        /// <returns>Whether the session id is valid</returns>
        public async Task<bool> ValidateSessId(string sessId) 
        {
            Uri uri = new Uri(Constants.RestUrl + "sessions/validate");
            bool result = false;
            try
            {
                StringContent data = new StringContent("sessId=" + sessId, Encoding.UTF8, "application/x-www-form-urlencoded");
                HttpResponseMessage response = await client.PostAsync(uri, data);
                // Could check body here but not necessary with current implementation.
                if (response.IsSuccessStatusCode)
                {
                    result = true;
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex;
            }

            return result;
        }

        public async Task<bool> SubmitOrder(Order order, Session sess) 
        {
            Uri uri = new Uri(Constants.RestUrl + "orders/new");
            bool result = false;
            try
            {
                var jsonData = new
                {
                    order = order,
                    sessId = sess.SessId
                };

                StringContent data = new StringContent(JsonConvert.SerializeObject(jsonData), Encoding.UTF8, "application/json");
                HttpResponseMessage response = await client.PostAsync(uri, data);
                // Could check body here but not necessary with current implementation.
                if (response.IsSuccessStatusCode)
                {
                    result = true;
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex;
            }

            return result;
        }
        async Task WarnUserCannotConnect() 
        {
            NetworkAccess networkState = Connectivity.NetworkAccess;

            var popup = new AlertDialog.Builder(Application.Context);
            AlertDialog alert = popup.Create();
            alert.SetTitle("Cannot connect to server");

            if (networkState == NetworkAccess.Internet)
            {
                // Can connect to intenet but cannot connect to server
                alert.SetMessage("Cannot reach server, please try again later.");
                alert.SetButton("Ok", (sender, args) =>
                {

                });

            }
            else 
            {
                // Canot connect to internet
                alert.SetMessage("Cannot connect to the internet, please connect and try again.");
                alert.SetButton("Ok", (sender, args) =>
                {

                });
            }
            alert.Show();
        }
    }
}