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

        public Item()
        {
            _tapCommand = new Command(async() => await OnTapped());
        }

        public ICommand TapCommand 
        {
            get { return _tapCommand; }
        }

        async Task OnTapped()
        {
            await App.Current.MainPage.Navigation.PushPopupAsync(new ItemPopupPage(this));
        }
    }
}
