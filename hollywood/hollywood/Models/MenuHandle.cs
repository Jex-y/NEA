using System;
using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;

namespace hollywood.Models
{
    public class MenuHandle
    {
        [JsonProperty("name")]
        public string Name { get; set; }
        [JsonProperty("url_name")]
        public string URLName { get; set; }
        [JsonProperty("description")]
        public string Description { get; set; }
        [JsonProperty("image")]
        public Uri ImageURI { get; set; }
    }
}
