using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using System.Windows.Input;
using System.ComponentModel;
using Xamarin.Forms;

using hollywood.Views;
using Rg.Plugins.Popup.Extensions;
using System.Threading.Tasks;
using hollywood.Services;
using System.Runtime.CompilerServices;

namespace hollywood.Models
{
    public class Item : INotifyPropertyChanged
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
        readonly ICommand _addCommand;
        readonly ICommand _removeCommand;
        readonly IContextService contextService;

        public event PropertyChangedEventHandler PropertyChanged;

        public Item()
        {
            contextService = DependencyService.Get<IContextService>();
            _tapCommand = new Command(async() => await OnTapped());
            _addNotesCommand = new Command(async () => await OnAddNotes());
            _addCommand = new Command(async () => await OnAdd());
            _removeCommand = new Command(async () => await OnRemove());
        }

        public decimal TotalPrice 
        {
            get { return Quantity * Price; }
        }

        public int Quantity {
            get {
                if (!(ThisItemOrder is null))
                {
                    return ThisItemOrder.num;
                }
                return 0;
            }

            set {
                if (value > 0)
                {
                    ThisItemOrder = new ItemOrder { num = value, notes = ThisItemOrder.notes };
                    NotifyPropertyChanged();
                    NotifyPropertyChanged("TotalPrice");
                }
                else if (value == 0) 
                {
                    removeItemOrder();
                }
            }
        }

        void NotifyPropertyChanged([CallerMemberName] String propertyName = "") 
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        public ICommand TapCommand 
        {
            get { return _tapCommand; }
        }

        public ICommand AddNotesCommand 
        {
            get { return _addNotesCommand; }
        }

        public ICommand AddCommand 
        {
            get { return _addCommand; }
        }

        public ICommand RemoveCommand 
        {
            get { return _removeCommand; }
        }

        ItemOrder ThisItemOrder
        {
            get 
            {
                ItemOrder result = null;
                if (contextService.Context.Basket.Items.ContainsKey(ID))
                {
                    result = contextService.Context.Basket.Items[ID];
                }
                return result;
            }

            set 
            {
                contextService.Context.Basket.Items[ID] = value;
            }
        }

        void removeItemOrder() 
        {
            // Not actually used as there is no way to refresh the view to no longer show the item.
            contextService.Context.Basket.Items.Remove(ID);
        }
        async Task OnTapped()
        {
            await App.Current.MainPage.Navigation.PushPopupAsync(new ItemPopupPage(this));
        }

        async Task OnAddNotes() 
        {
            
        }
        async Task OnAdd()
        {
            Quantity++;
            contextService.Context.Basket.Total += Price;
        }

        async Task OnRemove()
        {
            Quantity--;
            contextService.Context.Basket.Total -= Price;
        }
    }
}
