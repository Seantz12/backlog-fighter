<template>

<transition name="modal-transition">
  <div class="modal-vue">
    <div class="modal-container">
      <div class="modal-header">
        <slot name="header">
          <p>default header</p>
        </slot>
      </div>
      <div class="modal-content">
        <slot name="content"></slot>
      </div>
      <div class="modal-footer">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</transition>

</template>

<script>
export default {
  name: 'Modal',
};
</script>

<style scoped>
.modal-transition-enter-active, .modal-transition-leave-active {
  transition: opacity .5s;
}

.modal-transition-enter, .modal-transition-leave-to {
  opacity: 0;
}

.modal-vue {
  position: fixed;
  z-index: 99;
  background-color: rgba(0,0,0,0.4);
  left: 50%;
  top: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%);
}

.modal-vue div {
  background-color: #fefefe;
  /* margin: 15% auto; */
  /* padding: 25px; */
  /* border: 1px solid; */
}

.modal-container {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border: 3px solid;
}
</style>
