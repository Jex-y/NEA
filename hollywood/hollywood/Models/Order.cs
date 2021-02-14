using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;

namespace hollywood.Models
{
    public class Order
    {
        public Order() 
        {
            Items = new Dictionary<Guid, int>();
        }
        public event EventHandler OrderUpdated;

        [JsonProperty("items")]
        public Dictionary<Guid, int> Items { get; set; } // Hashmap

        [JsonProperty("notes")]
        public string notes { get; set; }

        public int getNum(Guid itemId) 
        {
            int num = 0;
            if (Items.ContainsKey(itemId)) 
            {
                num = Items[itemId];
            }

            return num;
        }

        public void updateNum(Guid itemId, int num) 
        {
            if (!(Items.ContainsKey(itemId) && Items[itemId] == num)) 
            {
                if (num == 0)
                {
                    Items.Remove(itemId);
                }
                else 
                {
                    Items[itemId] = num;
                }

                OnOrderUpdated(EventArgs.Empty);
            }
        }

        protected virtual void OnOrderUpdated(EventArgs args) 
        {
            EventHandler handler = OrderUpdated;
            handler?.Invoke(this, args);
        }
    }
}