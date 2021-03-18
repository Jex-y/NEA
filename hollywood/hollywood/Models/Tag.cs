using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace hollywood.Models
{
    public class Tag
    {
        public Tag() 
        {
            FilterBy = false;
        }
        [JsonProperty("id")]
        public Guid ID { get; set; }
        [JsonProperty("name")]
        public string Name { get; set; }
        [JsonProperty("icon")]
        public Uri IconURI { get; set; }

        public bool FilterBy { get; set; }
    }
}
