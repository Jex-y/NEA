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

// TODO: Remane MenuHandle, deal with case when cannot connect to server 
// i.e. create a popup with either server error message or connect to internet or server down
namespace hollywood.ViewModels
{
    public class MenuPageViewModel : BaseViewModel
    {
        readonly MenuHandle MenuHandle; // Change if u think of a better name
        Menu _menuData;
        bool _hasMenus = false;
        bool _isRefreshing = false;
        readonly ICommand _refreshCommand;
        DateTime MenusAge = DateTime.MinValue;

        public MenuPageViewModel(MenuHandle display = null)
        {
            if (display is null) // Handle top level case
            {
                Debug.WriteLine("Was null");
                display = new MenuHandle { 
                    Name="Menu", 
                    UrlName="", 
                    Description=null, 
                    ImageURI=null };
            }
            MenuHandle = display;
            Debug.WriteLine(MenuHandle.UrlName);
            Title = MenuHandle.Name;

            // Configure refresh command
            _refreshCommand = new Command(async () => await OnRefresh());
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

        public bool IsRefreshing
        {
            get { return _isRefreshing; }
            private set { SetProperty(ref _isRefreshing, value); }
        }

        public ICommand RefreshCommand 
        {
            get { return _refreshCommand;  }
        }

        async Task OnRefresh()
        {
            IsRefreshing = true;
            TimeSpan age = DateTime.Now - MenusAge;
            if (age.TotalSeconds > 1)
            {
                try
                {
                    MenuData = await App.ApiConnection.GetMenuAsync(MenuHandle);
                    MenusAge = DateTime.Now;
                }
                catch (Exception ex)
                {
                    Debug.WriteLine(@"\tERROR {0}", ex.Message);
                    throw ex;
                }
            }
            HasMenus = MenuData.SubMenus.Count > 0;
            IsRefreshing = false;
        }
    }
}