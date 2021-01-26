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
        public event EventHandler OrderUpdated;
        public Dictionary<Item, int> Items { get; set; } // Hashmap

        public string notes { get; set; }

        public int getNum(Item item) 
        {
            int num = 0;
            if (Items.ContainsKey(item)) 
            {
                num = Items[item];
            }

            return num;
        }

        public void updateNum(Item item, int num) 
        {
            if (!(Items.ContainsKey(item) && Items[item] == num)) 
            {
                if (num == 0)
                {
                    Items.Remove(item);
                }
                else 
                {
                    Items[item] = num;
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
