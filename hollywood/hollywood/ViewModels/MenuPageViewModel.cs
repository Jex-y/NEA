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
using Menu = hollywood.Models.Menu;

namespace hollywood.ViewModels
{
    public class MenuPageViewModel : BaseViewModel
    {
        public MenuPageViewModel(string title = "Menu")
        {
            Title = title;
        }

        Menu _menu;
        public Menu Menu
        {
            get { return _menu; }
            private set { SetProperty(ref _menu, value); }
        }

        bool _isRefreshing = false;
        public bool IsRefreshing
        {
            get { return _isRefreshing; }
            private set { SetProperty(ref _isRefreshing, value); }
        }

        DateTime MenusAge = DateTime.MinValue;

        public ICommand RefreshCommand => new Command(async () => await RefreshMenus());

        async Task RefreshMenus()
        {
            IsRefreshing = true;
            TimeSpan age = DateTime.Now - MenusAge;
            if (age.TotalSeconds > 1)
            {
                try
                {
                    Menu = await App.ApiConnection.GetMenuAsync(null);
                    MenusAge = DateTime.Now;
                }
                catch { }
            }
            IsRefreshing = false;
        }
    }
}