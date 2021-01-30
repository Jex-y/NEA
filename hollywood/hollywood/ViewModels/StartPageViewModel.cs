using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;
using Xamarin.Forms;
using hollywood.Views;
using hollywood.Services;
using hollywood.Models;

namespace hollywood.ViewModels
{
    public class StartPageViewModel
    {
        readonly IRestService restService;
        readonly ICommand _getSessIdCommand;
        readonly ICommand _startShellCommand;

        public StartPageViewModel() 
        {
            restService = DependencyService.Get<IRestService>();
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
            string sessId = await qrScanner.readCode();
            if (await ValidateSessId(sessId))
            {
                IContextService contextService = DependencyService.Get<IContextService>();
                contextService.Context.CurrentSession = new Session { SessId = new Guid(sessId) };
            }
            else
            {
                Debug.WriteLine("Could not scan qr code");
            }

        }
        void StartShell()
        {
            Device.BeginInvokeOnMainThread(() =>
            {
                App.Current.MainPage = new AppShell();
            });
            
        }

        async Task<bool> ValidateSessId(string sessId) 
        {
            return await restService.ValidateSessId(sessId);
        }
    }
}
