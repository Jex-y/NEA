using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Forms;
using hollywood.Views;
using hollywood.Services;

namespace hollywood.ViewModels
{
    public class StartPageViewModel
    {
        readonly ICommand _getSessIdCommand;
        readonly ICommand _startShellCommand;

        public StartPageViewModel() 
        {
            _startShellCommand = new Command(StartShell);
            _getSessIdCommand = new Command(async () => await GetSessId());
        }

        public ICommand StartShellCommand
        {
            get { return _startShellCommand; }
        }
        
        public ICommand GetSessIdCommand 
        {
            get { return _getSessIdCommand; }
        }

        async Task GetSessId() 
        {
            IQrScannerService qrScanner = DependencyService.Get<IQrScannerService>();
            await qrScanner.readCode();
            //string sessId = await qrScanner.readCode();
            //if (validateSessId(sessId))
            //{
            //    ((App)App.Current).ctx.CurrentSession.SessId = new Guid(sessId);
            //}
            //else 
            //{
            //    // Do something?
            //}

        }
        void StartShell()
        {
            Device.BeginInvokeOnMainThread(() =>
            {
                App.Current.MainPage = new AppShell();
            });
            
        }

        bool validateSessId(string sessId) 
        {
            // Validate is a guid and that it has been issued by the server recently. 
            // Needs a validate sessid api method
            return true;
        }
    }
}
