using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using hollywood.ViewModels;

namespace hollywood.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class PastOrderPage : ContentPage
    {
        readonly PastItemOrderPageViewModel vm;
        public PastOrderPage()
        {
            InitializeComponent();
            BindingContext = vm = new PastItemOrderPageViewModel();
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();
            vm.GetItems();
        }
    }
}