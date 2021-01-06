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
        public Guid ID { get; private set; }
        [JsonProperty("name")]
        public string Name { get; set; }
        [JsonProperty("description")]
        public string Description { get; set; }
        [JsonProperty("price")]
        public decimal Price { get; set; }
        [JsonProperty("tags")]
        public ObservableCollection<Tag> Tags { get; set; }
        [JsonProperty("image")]
        public Uri ImageURI { get; set; }
    }
}
