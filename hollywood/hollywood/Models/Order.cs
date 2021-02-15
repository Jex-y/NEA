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
            Items = new Dictionary<Guid, ItemOrder>();
        }


        Decimal _total;
        public event EventHandler OrderUpdated;

        [JsonProperty("items")]
        public Dictionary<Guid, ItemOrder> Items { get; set; } 

        public int getNum(Guid itemId) 
        {
            int num = 0;
            if (Items.ContainsKey(itemId)) 
            {
                num = Items[itemId].num;
            }

            return num;
        }

        public void updateNum(Guid itemId, int num) 
        {
            bool itemOrderExists = Items.ContainsKey(itemId);
            if (!(itemOrderExists && Items[itemId].num == num)) 
                // Doesn't yet exist or num is not the same as before
            {
                if (num == 0)
                {
                    Items.Remove(itemId);
                }
                else
                {
                    string notes = itemOrderExists ? Items[itemId].notes : "";
                    Items[itemId] = new ItemOrder { num=num, notes=notes };
                }

                OnOrderUpdated(EventArgs.Empty);
            }
        }

        public Decimal Total {
            get { return _total; }
            set 
            { 
                _total = value;
                OnOrderUpdated(EventArgs.Empty);
            }
        }

        public void TriggerUpdate() 
        {
            OnOrderUpdated(EventArgs.Empty);
        }

        protected virtual void OnOrderUpdated(EventArgs args) 
        {
            EventHandler handler = OrderUpdated;
            handler?.Invoke(this, args);
        }

    }
}