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
            
            BindingContext = vm = new MenuListViewModel();
            vm.RefreshMenus();
            InitializeComponent();
        }

        //public async void ButtonClicked(object sender, EventArgs args) 
        //{
        //    //Button SenderButton = (Button)sender;
        //    Debug.WriteLine("Am here");

        //} 
        readonly MenuListViewModel vm;
    }
}