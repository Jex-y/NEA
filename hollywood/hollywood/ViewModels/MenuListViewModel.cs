using hollywood.Models;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Essentials;
using Xamarin.Forms;

namespace hollywood.ViewModels
{
    public class MenuListViewModel : BaseViewModel
    {
        public MenuListViewModel()
        {
            Title = "Menu";
        }

        

        ObservableCollection<MenuHandle> menus = new ObservableCollection<MenuHandle>();
        public ObservableCollection<MenuHandle> Menus
        {
            get { return menus; }
            private set { SetProperty(ref menus, value); }
        }

        bool isRefreshing = false;
        public bool IsRefreshing
        {
            get { return isRefreshing; }
            private set { SetProperty(ref isRefreshing, value); }
        }

        DateTime MenusAge = DateTime.MinValue;

        public ICommand RefreshCommand => new Command(async () => await refreshMenus());

        async Task refreshMenus()
        {
            IsRefreshing = true;
            TimeSpan age = DateTime.Now - MenusAge;
            if (age.TotalSeconds > 1)
            {
                try
                {
                    Menus = await App.ApiConnection.GetMenusAsync();
                    MenusAge = DateTime.Now;
                }
                catch { }
            }
            IsRefreshing = false;
        }
    }
}