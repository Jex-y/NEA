using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

using hollywood.Models;
using System.Diagnostics;

namespace hollywood.Services
{
    class RestService : IRestService
    {
        HttpClient client;
        RestService() {
            client = new HttpClient();
        }

        public async Task<Menu> GetMenuDetailAsync(MenuHandle handle)
        {
            Uri uri = new Uri(Constants.RestUrl + "/menus/" + handle.url_name);
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
            }

            return menu;
        }

        public async Task<List<MenuHandle>> GetMenusAsync()
        {
            Uri uri = new Uri(Constants.RestUrl + "/menus/");
            List<MenuHandle> menus = new List<MenuHandle>();
            try
            {
                HttpResponseMessage response = await client.GetAsync(uri);
                if (response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    menus = JsonConvert.DeserializeObject<List<MenuHandle>>(content);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
            }

            return menus;
        }
    }
}
