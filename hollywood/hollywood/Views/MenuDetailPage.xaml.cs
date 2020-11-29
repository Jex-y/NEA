using hollywood.Models;
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
    //[XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class MenuDetailPage : ContentPage
    {
        readonly MenuDetailViewModel vm;
        public MenuDetailPage(MenuHandle handle)
        {
            InitializeComponent();
            BindingContext = vm = new MenuDetailViewModel(handle);
            vm.RefreshMenu();
        }
    }
}