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

        public async Task<MenuDetail> GetMenuDetailAsync(MenuHandle handle)
        {
            Uri uri = new Uri(Constants.RestUrl + "menus/" + handle.URLName);
            MenuDetail menu = null;
            try
            {
                HttpResponseMessage response = await client.GetAsync(uri);
                if (response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    menu = JsonConvert.DeserializeObject<MenuDetail>(content);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex;
            }

            return menu;
        }

        public async Task<ObservableCollection<MenuHandle>> GetMenusAsync()
        {
            Uri uri = new Uri(Constants.RestUrl + "menus/");
            ObservableCollection<MenuHandle> menus = new ObservableCollection<MenuHandle>();
            try
            {
                HttpResponseMessage response = await client.GetAsync(uri);
                if (response.IsSuccessStatusCode)
                {
                    string content = await response.Content.ReadAsStringAsync();
                    menus = JsonConvert.DeserializeObject<ObservableCollection<MenuHandle>>(content);
                }   
            }
            catch (Exception ex)
            {
                Debug.WriteLine(@"\tERROR {0}", ex.Message);
                throw ex;
            }

            return menus;
        }
    }
}
