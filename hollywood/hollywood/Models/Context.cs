using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace hollywood.Models
{
    public class Context
    {
        public Context() 
        {
            Basket = new Order();
        }
        [JsonProperty("basket")]
        public Order Basket {get; set;}

        [JsonProperty("session")]
        public Session CurrentSession { get; set; }
    }
}
