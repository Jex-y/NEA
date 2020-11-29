using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;

namespace hollywood.Models
{
    public class MenuDetail
    {
        [JsonProperty("menus")]
        public ObservableCollection<MenuHandle> SubMenus;
        [JsonProperty("items")]
        public ObservableCollection<Item> items;
    }
}
