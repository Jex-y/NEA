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
    public partial class FilterPopupPage : Rg.Plugins.Popup.Pages.PopupPage
    {
        public FilterPopupPage()
        {
            InitializeComponent();
        }
    }
}