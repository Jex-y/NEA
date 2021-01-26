using System;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using hollywood.Models;
using hollywood.Views;

namespace hollywood
{
    public partial class App : Application
    {
        public Context ctx;
        public App()
        {
            
            InitializeComponent();

            MainPage = new StartPage();
        }

        protected override void OnStart()
        {
            
        }

        protected override void OnSleep()
        {
            
        }

        protected override void OnResume()
        {

        }
    }
}
