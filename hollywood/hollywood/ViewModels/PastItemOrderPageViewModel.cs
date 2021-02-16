using hollywood.Models;
using hollywood.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Forms;

namespace hollywood.ViewModels
{
    class PastItemOrderPageViewModel : BaseViewModel
    {

        ObservableCollection<PastItemOrder> _items;
        readonly IRestService restService;
        readonly IContextService contextService;

        public PastItemOrderPageViewModel()
        {
            Title = "Orders";
            restService = DependencyService.Get<IRestService>();
            contextService = DependencyService.Get<IContextService>();
        }

        public ObservableCollection<PastItemOrder> Items
        {
            get { return _items; }
            set { SetProperty(ref _items, value); }
        }

        public decimal Total 
        {
            get 
            {
                decimal total = 0;
                if (!(Items is null)) 
                {
                    foreach (PastItemOrder item in Items)
                    {
                        total += item.Total;
                    }
                }
                

                return total;
            }
        }
        public async Task GetItems() 
        {
            Items = await restService.GetPastItems(contextService.Context.CurrentSession);
            OnPropertyChanged("Total");
        }
        

    }
}
