using System;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;
using hollywood.Services;
using hollywood.Views;

namespace hollywood
{
    public partial class App : Application
    {
        public static IRestService ApiConnection { get; private set; }
        public App()
        {
            InitializeComponent();
            ApiConnection = new RestService();

            MainPage = new AppShell();
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
