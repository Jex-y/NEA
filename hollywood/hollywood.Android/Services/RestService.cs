﻿using Android.App;
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

using hollywood.Services;
using hollywood.Models;

using Menu = hollywood.Models.Menu;
using Debug = System.Diagnostics.Debug;

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
                throw ex;
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
    }
}