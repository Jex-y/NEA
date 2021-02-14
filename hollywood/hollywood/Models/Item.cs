using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using System.Windows.Input;
using Xamarin.Forms;

using hollywood.Views;
using Rg.Plugins.Popup.Extensions;
using System.Threading.Tasks;
using hollywood.Services;

namespace hollywood.Models
{
    public class Item
    {
        [JsonProperty("id")]
        public Guid ID { get; set; }
        [JsonProperty("name")]
        public string Name { get; set; }
        [JsonProperty("description")]
        public string Description { get; set; }
        [JsonProperty("price")]
        public decimal Price { get; set; }
        [JsonProperty("tags")]
        public ObservableCollection<Tag> Tags { get; set; }
        [JsonProperty("image")]
        public Uri ImageURI { get; set; }

        readonly ICommand _tapCommand;
        readonly ICommand _addNotesCommand;

        public Item()
        {
            _tapCommand = new Command(async() => await OnTapped());
            _addNotesCommand = new Command(async () => await OnAddNotes());
        }

        public decimal TotalPrice 
        {
            get 
            {
                ItemOrder thisItemOrder = getItemOrder();
                if (!(thisItemOrder is null))
                {
                    return thisItemOrder.num * Price;
                }
                return 0;
            }
        }

        public ICommand TapCommand 
        {
            get { return _tapCommand; }
        }

        public ICommand AddNotesCommand 
        {
            get { return _addNotesCommand; }
        }

        async Task OnTapped()
        {
            await App.Current.MainPage.Navigation.PushPopupAsync(new ItemPopupPage(this));
        }

        async Task OnAddNotes() 
        {
            
        }



        ItemOrder getItemOrder() 
        {
            IContextService contextService = DependencyService.Get<IContextService>();
            ItemOrder result = null;
            if (contextService.Context.Basket.Items.ContainsKey(ID)) 
            {
                result = contextService.Context.Basket.Items[ID];
            }
            return result;
        }
    }
}
