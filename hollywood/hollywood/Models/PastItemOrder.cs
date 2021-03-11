using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace hollywood.Models
{
    public class PastItemOrder
    {
        [JsonProperty("name")]
        public string Name { get; set; }
        [JsonProperty("quantity")]
        public int Num { get; set; }
        [JsonProperty("notes")]
        public string Notes { get; set; }
        [JsonProperty("completed")]
        public bool Completed { get; set; }
        [JsonProperty("total")]
        public decimal Total { get; set; }
    }
}
