using hollywood.Models;
using hollywood.Services;
using hollywood.Views;
using Rg.Plugins.Popup.Extensions;
using System;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Forms;

using Menu = hollywood.Models.Menu;

namespace hollywood.ViewModels
{
    public class MenuPageViewModel : BaseViewModel
    {
        readonly MenuHandle MenuHandle; 
        Menu _menuData;
        bool _hasMenus = false;
        bool _hasItems = false;
        DateTime MenusAge = DateTime.MinValue;
        bool _isRefreshing = false;

        readonly ICommand _refreshCommand;
        readonly ICommand _searchCommand;
        readonly ICommand _filterCommand;
        readonly IRestService restService;
        readonly IContextService contextService;

        public MenuPageViewModel(MenuHandle display = null)
        {
            restService = DependencyService.Get<IRestService>();
            contextService = DependencyService.Get<IContextService>();

            if (display is null) // Handle top level case
            {
                display = new MenuHandle { 
                    Name="Menu", 
                    UrlName="", 
                    Description=null, 
                    ImageURI=null };
            }
            MenuHandle = display;
            Title = MenuHandle.Name;

            contextService.Context.Basket.OrderUpdated += Basket_OrderUpdated;
            _refreshCommand = new Command(async() => await OnRefresh());
            _searchCommand = new Command(async() => await OnSearch());
            _filterCommand = new Command(async () => await OnFilter());
        }

        void Basket_OrderUpdated(object sender, EventArgs e)
        {
            OnPropertyChanged("Total");
        }

        public void ForceUpdate() 
        {
            OnPropertyChanged("Total");
        }

        public Menu MenuData
        {
            get { return _menuData; }
            private set { SetProperty(ref _menuData, value); }
        }

        public bool HasMenus 
        {
            get { return _hasMenus; }
            private set { SetProperty(ref _hasMenus, value); }
        }

        public bool HasItems
        {
            get { return _hasItems; }
            private set { SetProperty(ref _hasItems, value); }
        }

        public bool IsRefreshing
        {
            get { return _isRefreshing; }
            private set { SetProperty(ref _isRefreshing, value); }
        }

        public ICommand RefreshCommand 
        {
            get { return _refreshCommand; }
        }

        public ICommand SearchCommand 
        {
            get { return _searchCommand; }
        }

        public ICommand FilterCommand
        {
            get { return _filterCommand; }
        }
        public string Total 
        {
            get { return string.Format("Total: {0:C2}", contextService.Context.Basket.Total); }
        }

        async Task OnRefresh()
        {
            IsRefreshing = true;
            TimeSpan age = DateTime.Now - MenusAge;
            if (age.TotalSeconds > 1)
            {
                try
                {
                    MenuData = await restService.GetMenuAsync(MenuHandle);
                    MenusAge = DateTime.Now;
                }
                catch (Exception ex)
                {
                    Debug.WriteLine(@"\tERROR {0}", ex.Message);
                    throw ex; 
                }
            }
            HasMenus = MenuData.SubMenus.Count > 0;
            HasItems = MenuData.Items.Count > 0;
            IsRefreshing = false;
        }

        async Task OnSearch()
        {
            await App.Current.MainPage.Navigation.PushAsync(new SearchPage());
        }

        async Task OnFilter()
        {
            await App.Current.MainPage.Navigation.PushPopupAsync(new FilterPopupPage());
        }
    }
}