using hollywood.Models;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Essentials;
using Xamarin.Forms;

namespace hollywood.ViewModels
{
    public class MenuListViewModel : BaseViewModel
    {
        List<MenuHandle> Menus;
        DateTime MenusAge;

        public MenuListViewModel()
        {
            Title = "Menu";
        }

        async Task<Boolean> RefreshMenus() {
            Boolean successful = false;
            try
            {
                Menus = await App.ApiConnection.GetMenusAsync();
                MenusAge = DateTime.Now;
                successful = true;
            }
            catch 
            { 
            }

            return successful;
        }
        public async Task<List<MenuHandle>> GetMenus() {
            TimeSpan age = DateTime.Now - MenusAge;

            if (age.TotalMinutes > 1) {
                await RefreshMenus();
            }

            return Menus;
        }

    }
}