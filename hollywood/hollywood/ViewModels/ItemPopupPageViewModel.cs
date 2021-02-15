using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

using Rg.Plugins.Popup.Extensions;

using Xamarin.Forms;
using hollywood.Models;
using hollywood.Services;

namespace hollywood.ViewModels
{
    class ItemPopupPageViewModel : BaseViewModel
    {
        readonly IContextService contextService;
        readonly Item _item;
        string _basketText;
        float _removeOpacity;
        float _addToBasketOpacity;
        int _numItems;
        //string _notes;

        readonly int startNum;

        readonly ICommand _closeCommand;
        readonly ICommand _addComamnd;
        readonly ICommand _removeCommand;
        readonly ICommand _addToBasketCommand;

        // If popup closed without add to basket, go back to initial order. 
        public ItemPopupPageViewModel(Item item)
        {
            _item = item;
            contextService = DependencyService.Get<IContextService>();

            startNum = contextService.Context.Basket.getNum(_item.ID);
            NumItems = startNum == 0 ? 1 : startNum;

            RemoveOpacity = 1.0f;
            AddToBasketOpacity = 1.0f;

            _closeCommand = new Command(async () => await OnClose());
            _addComamnd = new Command(async () => await OnAdd());
            _removeCommand = new Command(async () => await OnRemove());
            _addToBasketCommand = new Command(async () => await OnAddToBasket());
        }

        public Item Item
        {
            get { return _item; }
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
            if (NumItems == 1) 
            {
                RemoveOpacity = 1.0f;
            }
        }

        async Task OnRemove() 
        {
            if (NumItems > 0)
            {
                NumItems--;
            }
            if (NumItems == 0) 
            {
                RemoveOpacity = 0.4f;
            }
        }

        async Task OnAddToBasket() 
        {
            contextService.Context.Basket.updateNum(_item.ID, NumItems);

            await App.Current.MainPage.Navigation.PopPopupAsync();
        }

        void UpdateBasketText() 
        {
            if (NumItems > 0)
            {
                BasketText = string.Format("Add {0} to basket \u26AB {1:C2}",
                NumItems, NumItems * Item.Price);
            }
            else 
            {
                BasketText = "Remove from basket";
            }
            
        }
        
    }
}
