using hollywood.Models;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Forms;

namespace hollywood.ViewModels
{
    class MenuDetailViewModel : BaseViewModel
    {
        public MenuDetailViewModel(MenuHandle handle) 
        {
            this.handle = handle;            
            Title = handle.Name;
        }

        public async Task RefreshMenu()
        {
            IsRefreshing = true;
            TimeSpan age = DateTime.Now - MenuAge;
            if (age.TotalSeconds > 1)
            {
                try
                {
                    ViewMenu = await App.ApiConnection.GetMenuDetailAsync(handle);
                    MenuAge = DateTime.Now;
                }
                catch { }
            }
            IsRefreshing = false;
        }

        readonly MenuHandle handle;

        MenuDetail viewMenu;
        public MenuDetail ViewMenu 
        {
            get { return viewMenu; }
            private set { SetProperty(ref viewMenu, value); }
        }

        bool isRefreshing;
        public bool IsRefreshing
        {
            get { return isRefreshing; }
            private set { SetProperty(ref isRefreshing, value); }
        }

        DateTime MenuAge = DateTime.MinValue;

        public ICommand RefreshCommand => new Command(async () => await RefreshMenu());

        public string Currency = Constants.currency;
    }
}
