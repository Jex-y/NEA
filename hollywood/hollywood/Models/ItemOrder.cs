using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace hollywood.Models
{
    public class ItemOrder
    {
        [JsonProperty("num")]
        public int num { get; set; }
        [JsonProperty("notes")]
        public string notes { get; set; }
    }
}
