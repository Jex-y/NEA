using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace hollywood.Models
{
    public class Tag
    {
        [JsonProperty("id")]
        public Guid ID;
        [JsonProperty("name")]
        public string Name;
        [JsonProperty("icon")]
        public Uri IconURI;
    }
}
