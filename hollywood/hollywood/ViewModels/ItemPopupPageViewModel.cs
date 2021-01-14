using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

using Rg.Plugins.Popup.Extensions;

using hollywood.Models;
using Xamarin.Forms;

namespace hollywood.ViewModels
{
    class ItemPopupPageViewModel : BaseViewModel
    {
        readonly Item item;
        string _basketText;
        float _removeOpacity;
        float _addToBasketOpacity;
        int _numItems;

        readonly ICommand _closeCommand;
        readonly ICommand _addComamnd;
        readonly ICommand _removeCommand;
        readonly ICommand _addToBasketCommand;
        public ItemPopupPageViewModel(Item item)
        {
            this.item = item;

            RemoveOpacity = 0.4f;
            AddToBasketOpacity = 0.4f;

            NumItems = 1;

            _closeCommand = new Command(async() => await OnClose());
            _addComamnd = new Command(async() => await OnAdd());
            _removeCommand = new Command(async() => await OnRemove());
            _addToBasketCommand = new Command(async () => await OnAddToBasket());
        }

        public Item Item
        {
            get { return item; }
        }

        public string BasketText
        {
            get { return _basketText; }
            set { SetProperty(ref _basketText, value); }
        }

        public float RemoveOpacity 
        {
            get { return _removeOpacity; }
            set { SetProperty(ref _removeOpacity, value); }
        }
        public float AddToBasketOpacity
        {
            get { return _addToBasketOpacity; }
            set { SetProperty(ref _addToBasketOpacity, value); }
        }

        public int NumItems
        {
            get { return _numItems; }
            set { 
                SetProperty(ref _numItems, value);
                UpdateBasketText();
            }
        }

        public ICommand CloseCommand 
        {
            get { return _closeCommand; }
        }

        public ICommand AddCommand 
        {
             get { return _addComamnd; }
        }

        public ICommand RemoveCommand
        {
            get { return _removeCommand; }
        }

        public ICommand AddToBasketCommand
        {
            get { return _addToBasketCommand; }
        }
        async Task OnClose() 
        {
            await App.Current.MainPage.Navigation.PopPopupAsync();
        }

        async Task OnAdd() 
        {
            NumItems++;
            if (NumItems == 2) 
            {
                RemoveOpacity = 1.0f;
            }
        }

        async Task OnRemove() 
        {
            if (NumItems > 1) 
            {
                NumItems--;
            }
            
            if (NumItems == 1)
            {
                RemoveOpacity = 0.4f;
            }
        }

        async Task OnAddToBasket() 
        {

        }

        void UpdateBasketText() 
        {
            BasketText = string.Format("Add {0} to basket \u26AB {1:C2}", 
                NumItems, NumItems*Item.Price);
        }

        
    }
}
