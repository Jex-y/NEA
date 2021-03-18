using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using hollywood.ViewModels;
using hollywood.Models;
using System.Collections.ObjectModel;

namespace hollywood.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class FilterResultsPage : ContentPage
    {
        public FilterResultsPage(ObservableCollection<Item> items)
        {
            BindingContext = new FilterResultsPageViewModel(items);
            InitializeComponent();
        }
    }
}