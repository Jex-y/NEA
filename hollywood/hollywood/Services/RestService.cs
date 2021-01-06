using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

using hollywood.Models;
using System.Diagnostics;
using System.Collections.ObjectModel;

namespace hollywood.Services
{
    public class RestService : IRestService
    {
        readonly HttpClient client;
        public RestService() {
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
                throw ex;
            }

            return menu;
        }
    }
}
