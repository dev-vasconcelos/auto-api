using System;
using System.Linq;
using ${projectName}.Service.DTO.Interface;
using ${projectName}.Service.Models.Interface;

namespace ${projectName}.DTO.AbstractClass
{
    public abstract class AbstractModelDTO<T, ClassDto> : IDto
    {
        //public long? Id { get; set; }
        public long Id { get; set; }
        public virtual T ConvertFromDto(ClassDto generic)
        {
            var entity = (T)Activator.CreateInstance(typeof(T));
            var fields = generic.GetType().GetProperties().ToList();
            foreach (var item in fields)
            {
                var value = item.GetValue(generic);
                var property = entity.GetType().GetProperty(item.Name);
                if (property != null)
                {
                    if (value != null)
                    {
                        Type type2 = item.GetValue(generic).GetType();

                        Type type3 = typeof(IDto);

                        if (type2.GetInterfaces().Contains(typeof(IDto)))
                        {
                            dynamic vdto = generic.GetType().GetProperty(item.Name).GetValue(generic);
                            // dynamic vv = entity.GetType().GetProperty(item.Name).GetValue(entity);
                            value = vdto.ConvertFromDto(vdto);
                        }
                    }
                    entity.GetType().GetProperty(item.Name).SetValue(entity, value);
                }
            }

            return entity;
        }

        public virtual ObjectT ConvertFromDto<ObjectT, ObjectDTO>(ObjectDTO generic)
        {
            var entity = (ObjectT)Activator.CreateInstance(typeof(ObjectT));
            var fields = generic.GetType().GetProperties().ToList();
            foreach (var item in fields)
            {
                var value = item.GetValue(generic);
                var property = entity.GetType().GetProperty(item.Name);
                if (property != null)
                {
                    entity.GetType().GetProperty(item.Name).SetValue(entity, value);
                }
            }

            return entity;
        }

        public virtual ObjectDTO ConvertToDto<ObjectT, ObjectDTO>(ObjectT generic)
        {
            var entity = (ObjectDTO)Activator.CreateInstance(typeof(ObjectDTO));
            var fields = generic.GetType().GetProperties().ToList();
            foreach (var item in fields)
            {
                var value = item.GetValue(generic);
                var property = entity.GetType().GetProperty(item.Name);
                if (property != null)
                {
                    if (value != null)
                    {
                        Type type2 = item.GetValue(generic).GetType();

                        if (type2.GetInterfaces().Contains(typeof(IEntity)))
                        {
                            dynamic vdto = Activator.CreateInstance(entity.GetType().GetProperty(item.Name).GetGetMethod().ReturnType);
                            value = vdto.ConvertToDto(value, vdto);
                        }
                    }
                    entity.GetType().GetProperty(item.Name).SetValue(entity, value);
                }
            }

            return entity;
        }

        public virtual T2 ConvertToDto<T1, T2>(T1 generic, T2 dto)
        {
            var entity = (T2)Activator.CreateInstance(typeof(T2));
            var fields = generic.GetType().GetProperties().ToList();
            foreach (var item in fields)
            {
                var value = item.GetValue(generic);
                var property = entity.GetType().GetProperty(item.Name);
                if (property != null)
                {
                    if (value != null)
                    {
                        Type type2 = item.GetValue(generic).GetType();
                        if (type2.GetInterfaces().Contains(typeof(IEntity)))
                        {
                            dynamic vdto = Activator.CreateInstance(entity.GetType().GetProperty(item.Name).GetGetMethod().ReturnType);
                            value = vdto.ConvertToDto(vdto);
                        }
                        entity.GetType().GetProperty(item.Name).SetValue(entity, value);
                    }
                }
            }
            return entity;
        }

    }
}