using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;

namespace hollywood.Models
{
    public class Context
    {
        public Context() 
        {
            LastModified = DateTime.Now;
        }

        [JsonProperty("basket")]
        public Order Basket {get; set;}

        [JsonProperty("session")]
        public Session CurrentSession { get; set; }

        [JsonProperty("lastModifed")]
        public DateTime LastModified { get; set; }
    }
}
