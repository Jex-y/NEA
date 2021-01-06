using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;

namespace hollywood.Models
{
    public class Menu
    {
        [JsonProperty("menus")]
        public ObservableCollection<MenuHandle> SubMenus { get; set; }
        [JsonProperty("items")]
        public ObservableCollection<Item> Items { get; set; }
    }
}
