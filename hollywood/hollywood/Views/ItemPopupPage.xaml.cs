using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Xamarin.Forms;
using Xamarin.Forms.Xaml;

using hollywood.ViewModels;
using hollywood.Models;

namespace hollywood.Views
{
    [XamlCompilation(XamlCompilationOptions.Compile)]
    public partial class ItemPopupPage : Rg.Plugins.Popup.Pages.PopupPage
    {
        readonly ItemPopupPageViewModel vm;
        public ItemPopupPage(Item item)
        {
            InitializeComponent();
            BindingContext = vm = new ItemPopupPageViewModel(item);
        }
    }
}