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
            ctx = new Context(); // TODO: Check if there is a file already.
        }

        protected override void OnSleep()
        {
            // TODO: Save context
        }

        protected override void OnResume()
        {
            // Context should persist?
        }
    }
}
