using hollywood.ViewModels;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace hollywood.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class MenuListPage : ContentPage
    {
        readonly MenuListViewModel vm;
        public MenuListPage()
        {
            InitializeComponent();
            BindingContext = vm = new MenuListViewModel();
        }

        async void Test(object sender, EventArgs args) {
            await vm.GetMenus();
        }

    }
}