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
        readonly ICommand _closeSessionCommand;

        public PastItemOrderPageViewModel()
        {
            Title = "Orders";
            restService = DependencyService.Get<IRestService>();
            contextService = DependencyService.Get<IContextService>();

            _closeSessionCommand = new Command(async () => await OnCloseSession());
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

        public ICommand CloseSessionCommand 
        {
            get { return _closeSessionCommand; }
        }
        public async Task GetItems() 
        {
            Items = await restService.GetPastItems(contextService.Context.CurrentSession);
            OnPropertyChanged("Total");
        }

        async Task OnCloseSession() 
        {
            restService.CloseSession(contextService.Context.CurrentSession);
            contextService.Context.CurrentSession = null;
            // Display thank you page?
        }
    }
}
