using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using Xamarin.Forms;

namespace hollywood.Models
{
    public class Item
    {
        [JsonProperty("id")]
        public Guid ID;
        [JsonProperty("name")]
        public string Name;
        [JsonProperty("description")]
        public string Description;
        [JsonProperty("price")]
        public decimal Price;
        [JsonProperty("tags")]
        public ObservableCollection<Tag> Tags;
        [JsonProperty("image")]
        public Uri ImageURI;
    }
}
