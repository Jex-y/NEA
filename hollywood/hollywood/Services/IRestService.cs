using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using hollywood.Models;

namespace hollywood.Services
{
    interface IRestService
    {
        Task<List<MenuHandle>> GetMenusAsync ();

        Task<Menu> GetMenuDetailAsync(MenuHandle handle);

    }
}
