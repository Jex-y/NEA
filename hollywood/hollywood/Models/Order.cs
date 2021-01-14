using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;

namespace hollywood.Models
{
    // TODO: Deal with order notes
    public class Order
    {
        public Order() 
        {
            Items = new Dictionary<Item, int>();
        }
        public Dictionary<Item, int> Items { get; set; } // Hashmap

        public string notes { get; set; }
    }
}
