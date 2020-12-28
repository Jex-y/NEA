using hollywood.ViewModels;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace hollywood.Views
{
    public partial class MenuListPage : ContentPage
    {
        
        public MenuListPage()
        {
            InitializeComponent();
            BindingContext = vm = new MenuListViewModel();
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();

            vm.RefreshCommand.Execute(null);
        }
        readonly MenuListViewModel vm;
    }
}