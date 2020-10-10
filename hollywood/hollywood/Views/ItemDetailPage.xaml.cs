using System.ComponentModel;
using Xamarin.Forms;
using hollywood.ViewModels;

namespace hollywood.Views
{
    public partial class ItemDetailPage : ContentPage
    {
        public ItemDetailPage()
        {
            InitializeComponent();
            BindingContext = new ItemDetailViewModel();
        }
    }
}