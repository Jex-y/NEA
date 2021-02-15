using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

using hollywood.ViewModels;
using hollywood.Models;
using hollywood.Services;

namespace hollywood.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class MenuPage : ContentPage
    {
        readonly MenuPageViewModel vm;
        public MenuPage() 
        {
            InitializeComponent();
            BindingContext = vm = new MenuPageViewModel(null);
        }

        public MenuPage(MenuHandle display)
        {
            InitializeComponent();
            BindingContext = vm = new MenuPageViewModel(display);
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();

            vm.ForceUpdate();
            vm.RefreshCommand.Execute(null);
        }
    }
}