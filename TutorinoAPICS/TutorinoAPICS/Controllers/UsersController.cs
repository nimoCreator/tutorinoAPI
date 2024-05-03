﻿using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Data;
using System.Data.SqlClient;
using TutorinoAPICS.Models;

namespace TutorinoAPICS.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UsersController : ControllerBase
    {
        public readonly IConfiguration configuration;
        public UsersController(IConfiguration configuration)
        {
            this.configuration = configuration;
        }

        [HttpGet]
        [Route("getAllUsers")]
        public JsonResult GetUsers()
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("UsersAppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from users", con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            List<User> users = new List<User>();
            if (dataTable.Rows.Count > 0)
            {
                for (int i = 0; i < dataTable.Rows.Count; i++)
                {
                    User usr = new User();
                    usr.Id = Convert.ToInt32(dataTable.Rows[i]["uuid"]);
                    usr.UserName = Convert.ToString(dataTable.Rows[i]["name"]);
                    usr.UserSurname = Convert.ToString(dataTable.Rows[i]["surname"]);
                    users.Add(usr);
                }
            }
            if(users.Count>0)
            {
                JsonConvert.SerializeObject(users);
            }
        }
    }
}
