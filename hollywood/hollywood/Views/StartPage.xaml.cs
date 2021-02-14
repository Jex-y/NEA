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
    public partial class StartPage : ContentPage
    {
        StartPageViewModel vm;
        public StartPage()
        {
            InitializeComponent();
            BindingContext = vm = new StartPageViewModel();
        }
    }
}