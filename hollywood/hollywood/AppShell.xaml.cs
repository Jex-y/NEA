﻿using System;
using System.Collections.Generic;
using hollywood.ViewModels;
using hollywood.Views;
using Xamarin.Forms;

namespace hollywood
{
    public partial class AppShell : Xamarin.Forms.Shell
    {
        public AppShell()
        {
            InitializeComponent();
            //Routing.RegisterRoute(nameof(MenuPage), typeof(MenuPage));

            tab.CurrentItem = MenuPageTab;
        }

    }
}
