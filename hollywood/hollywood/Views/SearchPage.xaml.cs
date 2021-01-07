using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace hollywood.ViewModels
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class SearchPage : ContentPage
    {
        readonly SearchPageViewModel vm;
        public SearchPage()
        {
            InitializeComponent();
            BindingContext = vm = new SearchPageViewModel();
        }

        protected override void OnAppearing()
        {
            base.OnAppearing();

            vm.SearchCommand.Execute("");
        }
    }
}